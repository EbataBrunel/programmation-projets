package eajc.group.apv.dto;

import eajc.group.apv.enums.Gender;

public class GenderCountDto {

    private String gender;
    private Long count;

    public GenderCountDto(String gender, Long count) {
        this.gender = gender;
        this.count = count;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Long getCount() {
        return count;
    }

    public void setCount(Long count) {
        this.count = count;
    }
}
