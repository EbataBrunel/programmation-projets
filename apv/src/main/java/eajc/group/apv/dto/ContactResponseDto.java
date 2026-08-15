package eajc.group.apv.dto;

import java.time.LocalDateTime;
import java.util.UUID;


public class ContactResponseDto {
    private UUID publicId;
    private String lastName;
    private String firstName;
    private String email;
    private String phone;
    private String message;
    private Integer status;
    private LocalDateTime createdAt;

    public ContactResponseDto(){}

    public ContactResponseDto(UUID publicId, String lastName, String firstName, String email, String phone, String message, Integer status, LocalDateTime createdAt) {
        this.publicId = publicId;
        this.lastName = lastName;
        this.firstName = firstName;
        this.email = email;
        this.phone = phone;
        this.message = message;
        this.status = status;
        this.createdAt = createdAt;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getLastname() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
