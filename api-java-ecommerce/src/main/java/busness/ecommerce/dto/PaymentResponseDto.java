package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class PaymentResponseDto {
    private Long paymentId;
    private String clientSecret;
    private String paymentIntentId;
    private String status;
    private Double amount;
    private String mode;
    private String redirectUrl;
}
