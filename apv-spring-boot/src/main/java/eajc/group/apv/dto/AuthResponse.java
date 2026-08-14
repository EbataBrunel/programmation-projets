package eajc.group.apv.dto;

import java.util.List;
import java.util.UUID;

public class AuthResponse {
    private Long id;
    private UUID publicId;
    private String userName;
    private String email;
    private List<String> roles;

    public AuthResponse(){}

    public AuthResponse(Long id, UUID publicId, String userName, String email, List<String> roles) {
        this.id = id;
        this.publicId = publicId;
        this.userName = userName;
        this.email = email;
        this.roles = roles;
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

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public List<String> getRoles() {
        return roles;
    }

    public void setRoles(List<String> roles) {
        this.roles = roles;
    }
}

