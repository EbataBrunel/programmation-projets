package eajc.group.apv.dto;

public class UpdateContactStatusRequestDto {
    private Integer status;

    public UpdateContactStatusRequestDto(){}

    public UpdateContactStatusRequestDto(Integer status) {
        this.status = status;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }
}
