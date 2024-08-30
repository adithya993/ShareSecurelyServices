package uta.sharesecurelyservices.modal;

public class Users {
	private String signup_email;
	private String signup_fname;
	private String signup_lname;
	private String signup_confirmpassword;
	private String signup_group;
	
	public String getSignup_email() {
		return signup_email;
	}
	public void setSignup_email(String signup_email) {
		this.signup_email = signup_email;
	}
	public String getSignup_fname() {
		return signup_fname;
	}
	public void setSignup_fname(String signup_fname) {
		this.signup_fname = signup_fname;
	}
	public String getSignup_lname() {
		return signup_lname;
	}
	public void setSignup_lname(String signup_lname) {
		this.signup_lname = signup_lname;
	}
	public String getSignup_confirmpassword() {
		return signup_confirmpassword;
	}
	public void setSignup_confirmpassword(String signup_confirmpassword) {
		this.signup_confirmpassword = signup_confirmpassword;
	}
	public String getSignup_group() {
		return signup_group;
	}
	public void setSignup_group(String signup_group) {
		this.signup_group = signup_group;
	}
	@Override
	public String toString() {
		return "Users [signup_email=" + signup_email + ", signup_fname=" + signup_fname + ", signup_lname="
				+ signup_lname + ", signup_confirmpassword=" + signup_confirmpassword + ", signup_group=" + signup_group
				+ "]";
	}
	
}
