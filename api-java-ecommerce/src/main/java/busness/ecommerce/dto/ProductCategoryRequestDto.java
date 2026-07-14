package busness.ecommerce.dto;

import busness.ecommerce.entity.SubCategory;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductCategoryRequestDto {
    private String name;
    private Long subCategoryId;
}
