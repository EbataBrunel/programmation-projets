package busness.ecommerce.dto;

import busness.ecommerce.entity.Category;
import busness.ecommerce.enums.ProductSource;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductRequestDto {

    private String name;
    private String description;
    private Double price;
    private ProductSource source;
    private Long CategoryId;
    private Long SubCategoryId;
    private Long productCategoryId;
    private Long brandId;
}

