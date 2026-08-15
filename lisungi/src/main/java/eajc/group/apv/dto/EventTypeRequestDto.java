package eajc.group.apv.dto;

public class EventTypeRequestDto {
    private String name;

    public EventTypeRequestDto(){}

    public EventTypeRequestDto(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
