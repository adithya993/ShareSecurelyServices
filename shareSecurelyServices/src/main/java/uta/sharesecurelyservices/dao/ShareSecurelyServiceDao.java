package uta.sharesecurelyservices.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class ShareSecurelyServiceDao {
	private JdbcDatabaseConnection JdbcDatabaseConnection;
	
	public String registerUser(String email, String fname, String lname, String pass, String groups) {
		PreparedStatement stmt = null;
		JdbcDatabaseConnection = new JdbcDatabaseConnection();
		Connection conn = JdbcDatabaseConnection.databaseConnection();
		try {
			stmt = conn.prepareStatement("INSERT INTO USER_REGISTRATIONS (UserEmail, LastName, FirstName, UserPassword, UserGroups) VALUES (?,?,?,?,?)");
			stmt.setString(1, email);
			stmt.setString(2, lname);
			stmt.setString(3, fname);
			stmt.setString(4, pass);
			stmt.setString(5, groups);
			
			int row = stmt.executeUpdate();

            // rows affected
            System.out.println(row); //1
		    
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			System.out.println("Error in SQL Part 0");
			e.printStackTrace();
		} catch (Exception excep) {
			System.out.println("Error in SQL Part 1"); 
			excep.printStackTrace();
	               
		} finally {
			try {
	           if (stmt != null)
	              conn.close();
	        } catch (SQLException se) {}
	        try {
	           if (conn != null)
	              conn.close();
	        } catch (SQLException se) {
	           se.printStackTrace();
	        }  
		}
	      System.out.println("Please check it in the MySQL Table......... ……..");
		
		return "Success";
	}

	public JdbcDatabaseConnection getJdbcDatabaseConnection() {
		return JdbcDatabaseConnection;
	}

	public void setJdbcDatabaseConnection(JdbcDatabaseConnection jdbcDatabaseConnection) {
		JdbcDatabaseConnection = jdbcDatabaseConnection;
	}
}
