package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ProductImageResponseDto {
    private Long id;
    private String url;
    private boolean mainImage;
}
