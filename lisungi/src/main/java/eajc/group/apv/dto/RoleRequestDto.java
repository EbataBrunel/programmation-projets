package eajc.group.apv.dto;

public class RoleRequestDto {
    String name;

    public RoleRequestDto(){}

    public RoleRequestDto(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
