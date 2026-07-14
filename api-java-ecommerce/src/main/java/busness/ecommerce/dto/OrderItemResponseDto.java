package busness.ecommerce.dto;

import busness.ecommerce.entity.User;
import busness.ecommerce.enums.ProductSource;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class OrderItemResponseDto {
    private Long productVariationId;
    private String productName;
    private Double price; // Prix unitaire
    private String sku;
    private Integer quantity;
    private Double subtotal;
    private ProductSource source;
    private Long sellerId;
    private String sellerUsername;
}
