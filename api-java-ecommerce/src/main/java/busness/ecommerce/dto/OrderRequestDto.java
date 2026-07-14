package busness.ecommerce.dto;

import lombok.Data;

@Data
public class OrderRequestDto {
    private Long cartId;
    private String paymentMethod;
    private String shippingAddress;
}
