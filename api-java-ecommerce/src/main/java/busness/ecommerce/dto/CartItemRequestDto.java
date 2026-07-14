package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class CartItemRequestDto {
    private Long productVariantId;
    private Double price;
    private int quantity;
}
