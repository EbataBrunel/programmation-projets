package eajc.group.apv.dto;

import java.time.LocalDateTime;

public class RegulationRequestDto {

    private String name;

    private String description;

    private LocalDateTime updateAt;

    private Long userId;

    public RegulationRequestDto(){}

    public RegulationRequestDto(String name, String description, LocalDateTime updateAt, Long userId) {
        this.name = name;
        this.description = description;
        this.updateAt = updateAt;
        this.userId = userId;
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
}
