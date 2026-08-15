package eajc.group.apv.dto;

public class ViewRequestDto {

    private Long userId;

    public ViewRequestDto(){}

    public ViewRequestDto(Long userId) {
        this.userId = userId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }
}
