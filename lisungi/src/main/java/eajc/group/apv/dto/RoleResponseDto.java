package eajc.group.apv.dto;

import java.util.UUID;

public class RoleResponseDto {

    private UUID publicId;
    String name;

    public RoleResponseDto(){}

    public RoleResponseDto(UUID publicId, String name) {
        this.publicId = publicId;
        this.name = name;
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
}

