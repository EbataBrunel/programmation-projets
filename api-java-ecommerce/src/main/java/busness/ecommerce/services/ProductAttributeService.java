package busness.ecommerce.services;

import busness.ecommerce.dto.ProductAttributeRequestDto;
import busness.ecommerce.dto.ProductAttributeResponseDto;

import java.util.List;

public interface ProductAttributeService {
    ProductAttributeResponseDto create(ProductAttributeRequestDto dto);
    List<ProductAttributeResponseDto> getByVariant(Long variantId);
}
