package eajc.group.apv.dto;

import java.util.UUID;

public class ViewResponseDto {

    private Long id;

    private UUID publicId;

    private Long adminId;

    private Long userId;

    private String email;

    private String username;

    private Boolean status;

    public ViewResponseDto(){}

    public ViewResponseDto(Long id, UUID publicId, Long adminId, Long userId, String email, String username, Boolean status) {
        this.id = id;
        this.publicId = publicId;
        this.adminId = adminId;
        this.userId = userId;
        this.email = email;
        this.username = username;
        this.status = status;
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

    public Long getAdminId() {
        return adminId;
    }

    public void setAdminId(Long adminId) {
        this.adminId = adminId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Boolean getStatus() {
        return status;
    }

    public void setStatus(Boolean status) {
        this.status = status;
    }
}
