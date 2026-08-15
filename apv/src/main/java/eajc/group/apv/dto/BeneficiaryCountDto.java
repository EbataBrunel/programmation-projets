package eajc.group.apv.dto;

import java.util.UUID;

public class BeneficiaryCountDto {
    private Long id;
    private UUID publicId;
    private String name;
    private String type;
    private Long total;

    public BeneficiaryCountDto(){}

    public BeneficiaryCountDto(Long id, UUID publicId, String name, String type, Long total) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.type = type;
        this.total = total;
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

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Long getTotal() {
        return total;
    }

    public void setTotal(Long total) {
        this.total = total;
    }
}
