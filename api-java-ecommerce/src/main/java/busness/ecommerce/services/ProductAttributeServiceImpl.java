package busness.ecommerce.services;

import busness.ecommerce.dto.ProductAttributeRequestDto;
import busness.ecommerce.dto.ProductAttributeResponseDto;
import busness.ecommerce.entity.AttributeValue;
import busness.ecommerce.entity.ProductAttribute;
import busness.ecommerce.entity.ProductVariant;
import busness.ecommerce.mapper.ProductAttributeMapper;
import busness.ecommerce.repository.ProductAttributeRepository;
import busness.ecommerce.repository.ProductVariantRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductAttributeServiceImpl implements ProductAttributeService{

    private final ProductVariantRepository productVariantRepository;
    private final ProductAttributeRepository productAttributeRepository;
    private final ProductAttributeMapper productAttributeMapper;

    @Override
    public ProductAttributeResponseDto create(ProductAttributeRequestDto dto) {
        ProductVariant variant =
                productVariantRepository.findById(dto.getVariantId())
                        .orElseThrow(() ->
                                new RuntimeException("Variant not found"));

        AttributeValue value =
                productAttributeRepository.findById(dto.getAttributeValueId())
                        .orElseThrow(() -> new RuntimeException("Attribute value not found")).getAttributeValue();

        ProductAttribute pa = new ProductAttribute();
        pa.setVariant(variant);
        pa.setAttributeValue(value);

        return productAttributeMapper.toDto(
                productAttributeRepository.save(pa)
        );
    }

    @Override
    public List<ProductAttributeResponseDto> getByVariant(Long variantId) {
        ProductVariant variant =
                productVariantRepository.findById(variantId)
                        .orElseThrow();

        return productAttributeRepository
                .findByVariant(variant)
                .stream()
                .map(productAttributeMapper::toDto)
                .toList();
    }
}
