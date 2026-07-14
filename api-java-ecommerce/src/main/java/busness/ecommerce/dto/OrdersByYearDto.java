package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class OrdersByYearDto {
    private Integer year;
    private Long total;
}
