package uta.sharesecurelyservices.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import uta.sharesecurelyservices.modal.Users;
import uta.sharesecurelyservices.service.AesEncryption;
import uta.sharesecurelyservices.service.ShareSecurelyServicesService;

@Controller
public class ShareSecurelyServicesController {
	
	@GetMapping("")
	public String indexPage() {
		return "Index";
	}
	
	@GetMapping("/")
	public String loginPage() {
		return "UserLogin";
	}
	
	@PostMapping("/registerNewUser")
    public String userRegistration(@ModelAttribute Users newuser) {
		System.out.print(newuser.toString());
        return "User Login";
    }
	
	@RequestMapping("/SaveUserRecord")
    @ResponseBody
    public String registerUser(@RequestParam("email") String email, @RequestParam("fname") String fname, @RequestParam("lname") String lname, @RequestParam("pass") String pass, @RequestParam("groups") String groups) {
		System.out.print(email + " {,.} " + fname + " {,.} " + lname + " {,.} " + pass + " {,.} " + groups);
		ShareSecurelyServicesService serv = new ShareSecurelyServicesService();
		return serv.registerUser(email, fname, lname, pass, groups);		
    }
}
