package eajc.group.apv.dto;

import eajc.group.apv.enums.Gender;

import java.time.LocalDate;

public class UserProfileRequestDto {

    private String firstName;
    private String lastName;
    private Gender gender;
    private String phone;
    private String address;
    private Long userId;
    private String country;
    private String city;
    private String borough;
    private String profession;
    private String photo;

    public UserProfileRequestDto(){}

    public UserProfileRequestDto(String firstName, String lastName, Gender gender, String phone, String address, Long userId, String country, String city, String borough, String profession, String photo) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.phone = phone;
        this.address = address;
        this.userId = userId;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.profession = profession;
        this.photo = photo;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getBorough() {
        return borough;
    }

    public void setBorough(String borough) {
        this.borough = borough;
    }

    public String getProfession() {
        return profession;
    }

    public void setProfession(String profession) {
        this.profession = profession;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }
}
