package eajc.group.apv.dto;

import lombok.*;

import java.util.List;
import java.util.UUID;

public class UserResponseDto {
    public Long id;
    private UUID publicId;
    private String username;
    private String email;
    private boolean enabled;
    private UserProfileResponseDto userProfile;
    private List<RoleResponseDto> roles;

    public UserResponseDto(){}

    public UserResponseDto(Long id, UUID publicId, String username, String email, boolean enabled, UserProfileResponseDto userProfile, List<RoleResponseDto> roles) {
        this.id = id;
        this.publicId = publicId;
        this.username = username;
        this.email = email;
        this.enabled = enabled;
        this.userProfile = userProfile;
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

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public List<RoleResponseDto> getRoles() {
        return roles;
    }

    public void setRoles(List<RoleResponseDto> roles) {
        this.roles = roles;
    }

    public UserProfileResponseDto getUserProfile() {
        return userProfile;
    }

    public void setUserProfile(UserProfileResponseDto userProfile) {
        this.userProfile = userProfile;
    }
}
