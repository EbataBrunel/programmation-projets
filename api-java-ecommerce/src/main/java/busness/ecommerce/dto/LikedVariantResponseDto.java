package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LikedVariantResponseDto {
    Long variantId;
    String productName;
    String sku;
    Double price;
    String imageUrl;
}
