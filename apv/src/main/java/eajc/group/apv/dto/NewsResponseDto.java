package eajc.group.apv.dto;

import java.time.LocalDateTime;
import java.util.UUID;

public class NewsResponseDto {

    private UUID publicId;

    private String title;

    private String content;

    private String photo;

    private Boolean status;

    private LocalDateTime createdAt;

    public NewsResponseDto(){}

    public NewsResponseDto(UUID publicId, String title, String content, String photo, Boolean status, LocalDateTime createdAt) {
        this.publicId = publicId;
        this.title = title;
        this.content = content;
        this.photo = photo;
        this.status = status;
        this.createdAt = createdAt;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public Boolean getStatus() {
        return status;
    }

    public void setStatus(Boolean status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
