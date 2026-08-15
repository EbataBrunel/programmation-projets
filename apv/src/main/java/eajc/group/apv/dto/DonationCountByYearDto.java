package eajc.group.apv.dto;

public class DonationCountByYearDto {
    private Integer year;
    private Long count;

    public DonationCountByYearDto(Integer year, Long count) {
        this.year = year;
        this.count = count;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(Integer year) {
        this.year = year;
    }

    public Long getCount() {
        return count;
    }

    public void setCount(Long count) {
        this.count = count;
    }
}
