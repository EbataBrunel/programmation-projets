package busness.ecommerce.dto;

import busness.ecommerce.enums.ProductSource;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductResponseDto {
    private Long id;
    private String name;
    private String description;
    private Double price;
    private ProductSource source;
    private Long categoryId;
    private Long subCategoryId;
    private Long productCategoryId;
    private Long ownerId;
    private Long brandId;
    private String brandName;
    private List<ProductImageResponseDto> images;

}
