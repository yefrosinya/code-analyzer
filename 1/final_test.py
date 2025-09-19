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
    
    print("=== ФИНАЛЬНЫЙ ТЕСТ ===")
    print()
    
    # Показываем проблемные операторы
    print("ПРОВЕРКА ПРОБЛЕМНЫХ ОПЕРАТОРОВ:")
    arrow_count = parser.operators_dict.get('->', 0)
    equals_count = parser.operators_dict.get('==', 0)
    or_count = parser.operators_dict.get('||', 0)
    arrow_equals_count = parser.operators_dict.get('=>', 0)
    
    print(f"Оператор '->': {arrow_count} раз")
    print(f"Оператор '==': {equals_count} раз")
    print(f"Оператор '||': {or_count} раз")
    print(f"Оператор '=>': {arrow_equals_count} раз")
    
    # Проверяем, есть ли отдельные символы
    single_arrow = parser.operators_dict.get('-', 0)
    single_equals = parser.operators_dict.get('=', 0)
    single_or = parser.operators_dict.get('|', 0)
    single_greater = parser.operators_dict.get('>', 0)
    
    print(f"Отдельный символ '-': {single_arrow} раз")
    print(f"Отдельный символ '=': {single_equals} раз")
    print(f"Отдельный символ '|': {single_or} раз")
    print(f"Отдельный символ '>': {single_greater} раз")
    
    print()
    print("=== РЕЗУЛЬТАТ ===")
    
    # Проверяем результаты
    success = True
    if single_arrow > 0:
        print("❌ ОШИБКА: Отдельные символы '-' не должны считаться!")
        success = False
    if single_or > 0:
        print("❌ ОШИБКА: Отдельные символы '|' не должны считаться!")
        success = False
    if single_greater > 0:
        print("❌ ОШИБКА: Отдельные символы '>' не должны считаться!")
        success = False
    
    if success:
        print("✅ УСПЕХ: Все операторы обрабатываются правильно!")
        print(f"   - '->': {arrow_count} раз (только целиком)")
        print(f"   - '==': {equals_count} раз (правильно, в коде нет)")
        print(f"   - '||': {or_count} раз (только целиком)")
        print(f"   - '=>': {arrow_equals_count} раз (только целиком)")
        print(f"   - Отдельные символы: 0 раз")

if __name__ == "__main__":
    main()
