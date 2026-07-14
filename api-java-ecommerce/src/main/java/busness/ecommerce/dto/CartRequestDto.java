package busness.ecommerce.dto;

import lombok.Data;

@Data
public class CartRequestDto {
    private Long productVariantId;
    private Integer quantity;
}
