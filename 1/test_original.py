#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from script import HalsteadParser

# Оригинальный PHP код
test_code = """<?php
class UserManager {
    private $db;
    private $users = [] ;

    public function __construct ( $database ) {
        $this->db = $database ;
        $this->loadUsers() ;
}

    public function loadUsers() {
        while ( $row = $result->fetch_assoc() ) {
            $this->users[ $row['id']] = $row;
        }
    }

    public function getUserById($userId) {
        return $this -> users[ $userId ] ?? null;
    }

    public function addUser( $name, $email, $role = 'user') {
        if (!filter_var( $email, FILTER_VALIDATE_EMAIL) || strlen( $name) < 2) {
            throw new Exception( " Invalid input " ) ;
        }
        $stmt = $this->db->prepare( " INSERT INTO users (name, email, role) VALUES ( ? , ? , ? ) " );
        $stmt->bind_param( " sss " , $name, $email, $role) ;
        
        if ( $stmt -> execute () ) {
            $newUserId = $this-> db -> insert_id;
            $this->users[ $newUserId] = [' name ' => $name , ' email ' => $email, ' role ' => $role] ;
            return $newUserId;
        }
        return false;
    }

    public function updateUser( $userId, $data) {
        if ( ! isset( $this-> users [ $userId ] ) ) {
            throw new Exception (" User not found ") ;
        }
        $allowed = [ ' name ', 'email', 'role' ] ;
        $updateData = array_intersect_key( $data , array_flip ( $allowed) ) ;
        if ( empty ( $updateData ) ) return false;

        $setClause = implode ( " , " , array_map ( fn ( $f ) => " $f = ? ", array_keys ( $updateData ) ) ) ;
        $params = array_merge ( array_values ( $updateData ) , [ $userId] ) ;
        $types = str_repeat( "s" , count( $updateData) ) . " i ";

        $stmt->bind_param( $types, ... $params) ;
        if ( $stmt->execute( ) ) {
         
   $this->users[ $userId] = array_merge( $this->users[ $userId] , $updateData) ; 
            return true ;
        }
        return false ;
    }

    public function deleteUser( $userId) {
        if ( ! isset( $this->users[ $userId] ) ) return false ;
        
        $stmt->bind_param("i", $userId) ;
        
        if ( $stmt->execute() ) {
            unset( $this->users[ $userId] ) ;
            return true;
        }
        return false;
    }

    public function getUsersByRole ( $role) {
        return array_filter( $this->users, fn( $user) => $user['role'] === $role) ;
    }
}

$db = new mysqli( " localhost ", " user ", " pass ", " test_db ") ;
$manager = new UserManager( $db) ;
try {
    $id = $manager->addUser("John", "john@mail.com", "admin") ;
    echo "User $id added\n" ;
    
    $user = $manager->getUserById ( $id ) ;
    if ( $user) echo "Found: {$user['name']}\n"; 

    $manager->updateUser( $id, ['name' => ' John Updated '] ) ;
    echo "User updated \n " 
    $admins = $manager->getUsersByRole('admin') ;
    echo "Admins: " . count( $admins) . "\n";

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>"""

def main():
    parser = HalsteadParser()
    parser.parse_code(test_code)
    
    print("=== ТЕСТ ОРИГИНАЛЬНОГО КОДА ===")
    print()
    
    print(f"eta1 (уникальные операторы): {parser.eta1}")
    print(f"N1 (общее количество операторов): {parser.N1}")
    print(f"eta2 (уникальные операнды): {parser.eta2}")
    print(f"N2 (общее количество операндов): {parser.N2}")
    print()
    
    print("Проверка:")
    print(f"  eta1 == len(operators_dict): {parser.eta1 == len(parser.operators_dict)}")
    print(f"  N1 == sum(operators_dict.values()): {parser.N1 == sum(parser.operators_dict.values())}")
    print(f"  eta2 == len(operands_dict): {parser.eta2 == len(parser.operands_dict)}")
    print(f"  N2 == sum(operands_dict.values()): {parser.N2 == sum(parser.operands_dict.values())}")
    
    print()
    print("Количество операторов в словаре:", len(parser.operators_dict))
    print("Количество операндов в словаре:", len(parser.operands_dict))

if __name__ == "__main__":
    main()
