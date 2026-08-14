package eajc.group.apv.dto;

import java.time.LocalDateTime;
import java.util.UUID;

public class RegulationResponseDto {

    private UUID publicId;

    private String name;

    private String description;

    private LocalDateTime createdAt;

    private LocalDateTime updateAt;

    private Long userId;

    private String userLastName;

    private String userFirstName;

    public RegulationResponseDto(){}

    public RegulationResponseDto(UUID publicId, String name, LocalDateTime createdAt, String description, LocalDateTime updateAt, Long userId, String userLastName, String userFirstName) {
        this.publicId = publicId;
        this.name = name;
        this.createdAt = createdAt;
        this.description = description;
        this.updateAt = updateAt;
        this.userId = userId;
        this.userLastName = userLastName;
        this.userFirstName = userFirstName;
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdateAt() {
        return updateAt;
    }

    public void setUpdateAt(LocalDateTime updateAt) {
        this.updateAt = updateAt;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUserLastName() {
        return userLastName;
    }

    public void setUserLastName(String userLastName) {
        this.userLastName = userLastName;
    }

    public String getUserFirstName() {
        return userFirstName;
    }

    public void setUserFirstName(String userFirstName) {
        this.userFirstName = userFirstName;
    }
}
