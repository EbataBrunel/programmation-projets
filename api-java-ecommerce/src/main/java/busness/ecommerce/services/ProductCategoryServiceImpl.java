package busness.ecommerce.services;

import busness.ecommerce.dto.ProductCategoryRequestDto;
import busness.ecommerce.dto.ProductCategoryResponseDto;
import busness.ecommerce.dto.VariantProductCategoryCountResponseDto;
import busness.ecommerce.entity.ProductCategory;
import busness.ecommerce.entity.SubCategory;
import busness.ecommerce.enums.Gender;
import busness.ecommerce.mapper.ProductCategoryMapper;
import busness.ecommerce.repository.ProductCategoryRepository;
import busness.ecommerce.repository.SubCategoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ProductCategoryServiceImpl implements  ProductCategoryService{

    private final ProductCategoryRepository productCategoryRepository;
    private final SubCategoryRepository subCategoryRepository;
    private final ProductCategoryMapper productCategoryMapper;

    @Override
    public ProductCategoryResponseDto createProductCategory(ProductCategoryRequestDto dto) {

        SubCategory subCategory = subCategoryRepository.findById(dto.getSubCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));
        ProductCategory productCategory = productCategoryMapper.toEntity(dto, subCategory);
        ProductCategory productCategorySave = productCategoryRepository.save(productCategory);

        return productCategoryMapper.toDto(productCategorySave);
    }

    @Override
    public List<ProductCategoryResponseDto> getAllProductCategories() {
        return productCategoryRepository.findAll()
                .stream()
                .map(productCategoryMapper::toDto)
                .toList();
    }

    @Override
    public ProductCategoryResponseDto getProductCategoryById(Long id) {
        ProductCategory productCategory = productCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("ProductCategory not found"));

        return productCategoryMapper.toDto(productCategory);
    }

    @Override
    public List<ProductCategoryResponseDto> getProductCategoriesBySubCategory(Long subCategoryId) {
        return productCategoryRepository.findBySubCategoryId(subCategoryId)
                .stream()
                .map(productCategoryMapper::toDto)
                .toList();
    }

    @Override
    public ProductCategoryResponseDto updateProductCategory(Long id, ProductCategoryRequestDto dto) {
        ProductCategory productCategory = productCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("ProductCategory not found"));

        SubCategory subCategory = subCategoryRepository.findById(dto.getSubCategoryId())
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));

        productCategory.setName(dto.getName());
        productCategory.setSubCategory(subCategory);

        return productCategoryMapper.toDto(productCategoryRepository.save(productCategory));
    }

    @Override
    public List<VariantProductCategoryCountResponseDto> countVariantsProductCategoryByGenderAndSubCategory(Gender gender, Long subCategoryId) {
        List<Object[]> results = productCategoryRepository.countVariantsProductCategoryByGenderAndSubCategory(gender, subCategoryId);
        return results
                .stream()
                .map(row -> new VariantProductCategoryCountResponseDto(
                    ((Number)row[0]).longValue(),
                        (String)row[1],
                        ((Number)row[2]).longValue()
                ))
                .collect(Collectors.toList());
    }

    @Override
    public void deleteProductCategory(Long id) {
        ProductCategory productCategory = productCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("ProductCategory not found"));

        productCategoryRepository.delete(productCategory);
    }
}
