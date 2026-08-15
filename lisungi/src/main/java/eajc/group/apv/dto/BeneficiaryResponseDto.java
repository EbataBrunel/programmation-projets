package eajc.group.apv.dto;

import java.time.LocalDate;
import java.util.UUID;

public class BeneficiaryResponseDto {

    private Long id;

    private UUID publicId;

    private String name;

    private String phone;

    private  String email;

    private String address;

    private String country;

    private String city;

    private String borough;

    private String type;

    private LocalDate dateExistence;

    public BeneficiaryResponseDto(){}

    public BeneficiaryResponseDto(Long id, UUID publicId, String phone, String name, String email, String address, String country, String city, String borough, String type, LocalDate dateExistence) {
        this.id = id;
        this.publicId = publicId;
        this.phone = phone;
        this.name = name;
        this.email = email;
        this.address = address;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.type = type;
        this.dateExistence = dateExistence;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
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

    public String getBorough() {
        return borough;
    }

    public void setBorough(String borough) {
        this.borough = borough;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public LocalDate getDateExistence() {
        return dateExistence;
    }

    public void setDateExistence(LocalDate dateExistence) {
        this.dateExistence = dateExistence;
    }
}
