package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Builder
public class OrderResponseDto {

    private Long id;
    private Double total;
    private String status;
    private LocalDateTime createdAt;
    private List<OrderItemResponseDto> items;
}

