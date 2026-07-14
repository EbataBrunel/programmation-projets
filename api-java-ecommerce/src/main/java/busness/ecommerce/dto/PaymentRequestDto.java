package busness.ecommerce.dto;

import busness.ecommerce.enums.ModePayment;
import lombok.Data;

@Data
public class PaymentRequestDto {
    private Long orderId;
    private ModePayment mode;
}
