package busness.ecommerce.dto;

import busness.ecommerce.enums.ModePayment;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Builder
public class PaymentListDto {
    private Long id;
    private Double amount;
    private String status;
    private ModePayment mode;
    private LocalDateTime createdAt;
    private Long orderId;
}
