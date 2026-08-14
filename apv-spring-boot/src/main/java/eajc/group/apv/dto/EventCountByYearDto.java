package eajc.group.apv.dto;


public class EventCountByYearDto {

    private Integer year;
    private Long count;

    public EventCountByYearDto(Integer year, Long count) {
        this.year = year;
        this.count = count;
    }

    public Integer getYear() {
        return year;
    }

    public Long getCount() {
        return count;
    }

}
