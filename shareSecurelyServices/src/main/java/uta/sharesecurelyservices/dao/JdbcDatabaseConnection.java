package uta.sharesecurelyservices.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;

public class JdbcDatabaseConnection {
	
	public Connection databaseConnection() {
		System.out.println("-------- MySQL JDBC Connection Testing ------");
		
		//System.out.println(env.toString());
		
		JdbcDatabaseConnection jdbc = new JdbcDatabaseConnection();
		
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			System.out.println("Where is your MySQL JDBC Driver?");
			e.printStackTrace();
			return null;

		}
		System.out.println("MySQL JDBC Driver Registered!");
		Connection connection = null;
		try {
			connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/sharesecureservices", "root", "Meg@bite001");
		} catch (SQLException e) {
			System.out.println("Connection Failed! Check output console");
			e.printStackTrace();
			return null;
		}
		if (connection != null) {
			System.out.println("You made it, take control of your database now!\n");
			return connection;
		} else {
			System.out.println("Failed to make connection!");
		}
		return null;
	}
}
