package eajc.group.apv.dto;

import java.time.LocalDate;
import java.util.UUID;

public class UserProfileResponseDto {

    private UUID publicId;
    private String firstName;
    private String gender;
    private String lastName;
    private String phone;
    private String address;
    private String country;
    private String city;
    private String borough;
    private String  profession;
    private String photo;
    private LocalDate registrationDate;
    private String reasonRemoval;

    private Long userId;
    private String userName;
    private String userEmail;

    public UserProfileResponseDto(){}

    public UserProfileResponseDto(UUID publicId, String firstName, String gender, String lastName, String phone, String address, String country, String city, String borough, String profession, String photo, LocalDate registrationDate, String reasonRemoval, Long userId, String userName, String userEmail) {
        this.publicId = publicId;
        this.firstName = firstName;
        this.gender = gender;
        this.lastName = lastName;
        this.phone = phone;
        this.address = address;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.profession = profession;
        this.photo = photo;
        this.registrationDate = registrationDate;
        this.reasonRemoval = reasonRemoval;
        this.userId = userId;
        this.userName = userName;
        this.userEmail = userEmail;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
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

    public LocalDate getRegistrationDate() {
        return registrationDate;
    }

    public void setRegistrationDate(LocalDate registrationDate) {
        this.registrationDate = registrationDate;
    }

    public String getReasonRemoval() {
        return reasonRemoval;
    }

    public void setReasonRemoval(String reasonRemoval) {
        this.reasonRemoval = reasonRemoval;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public void setUserEmail(String userEmail) {
        this.userEmail = userEmail;
    }
}

