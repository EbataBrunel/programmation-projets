package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class OrdersByMonthDto {
    private Integer month;
    private Long total;
}
