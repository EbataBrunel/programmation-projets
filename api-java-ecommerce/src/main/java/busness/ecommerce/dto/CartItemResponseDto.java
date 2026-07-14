package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class CartItemResponseDto {
    private Long id;

    private Long productVariantId;
    private String productName;
    private String productImageUrl;
    private Double price;
    private Integer quantity;
    private Double subTotal;
}
