package uta.sharesecurelyservices.service;

import uta.sharesecurelyservices.dao.ShareSecurelyServiceDao;

public class ShareSecurelyServicesService {
	private ShareSecurelyServiceDao dao;
	
	public String registerUser(String email, String fname, String lname, String pass, String groups) {
		AesEncryption obj = new AesEncryption();
		dao = new ShareSecurelyServiceDao();
		return dao.registerUser(email, fname, lname, obj.encrypt(pass), groups);
	}
}
