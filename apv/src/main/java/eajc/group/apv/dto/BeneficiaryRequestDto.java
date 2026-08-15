package eajc.group.apv.dto;

import eajc.group.apv.enums.BeneficiaryType;

import java.time.LocalDate;

public class BeneficiaryRequestDto {

    private BeneficiaryType type;

    private String name;

    private String phone;

    private  String email;

    private String address;

    private String country;

    private String city;

    private String borough;

    private LocalDate dateExistence;

    BeneficiaryRequestDto(){}

    public BeneficiaryRequestDto(BeneficiaryType type, String name, String phone, String email, String address, String country, String city, String borough, LocalDate dateExistence) {
        this.type = type;
        this.name = name;
        this.phone = phone;
        this.email = email;
        this.address = address;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.dateExistence = dateExistence;
    }

    public BeneficiaryType getType() {
        return type;
    }

    public void setType(BeneficiaryType type) {
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
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

    public LocalDate getDateExistence() {
        return dateExistence;
    }

    public void setDateExistence(LocalDate dateExistence) {
        this.dateExistence = dateExistence;
    }
}
