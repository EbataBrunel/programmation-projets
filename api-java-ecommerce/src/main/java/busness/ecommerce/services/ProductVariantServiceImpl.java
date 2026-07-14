package busness.ecommerce.services;

import busness.ecommerce.dto.BrandVariantCountResponseDto;
import busness.ecommerce.dto.ProductVariantRequestDto;
import busness.ecommerce.dto.ProductVariantResponseDto;
import busness.ecommerce.dto.ProductVariantUpdateRequestDto;
import busness.ecommerce.entity.AttributeValue;
import busness.ecommerce.entity.Product;
import busness.ecommerce.entity.ProductAttribute;
import busness.ecommerce.entity.ProductVariant;
import busness.ecommerce.enums.Gender;
import busness.ecommerce.mapper.ProductVariantMapper;
import busness.ecommerce.repository.AttributeValueRepository;
import busness.ecommerce.repository.ProductAttributeRepository;
import busness.ecommerce.repository.ProductRepository;
import busness.ecommerce.repository.ProductVariantRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ProductVariantServiceImpl implements ProductVariantService{

    private final ProductRepository productRepository;
    private final ProductVariantRepository productVariantRepository;
    private final AttributeValueRepository attributeValueRepository;
    private final ProductAttributeRepository productAttributeRepository;
    private final ProductVariantMapper productVariantMapper;
    @Override
    public ProductVariantResponseDto create(ProductVariantRequestDto dto) {
        Product product = productRepository.findById(dto.getProductId())
                .orElseThrow(() -> new RuntimeException("Product not found"));

        ProductVariant variant = new ProductVariant();
        variant.setPrice(dto.getPrice());
        variant.setStock(dto.getStock());
        variant.setGender(dto.getGender());
        variant.setProduct(product);

        productVariantRepository.save(variant);

        List<AttributeValue> values = new ArrayList<>();
        for (Long valueId : dto.getAttributes()) {

            AttributeValue value = attributeValueRepository.findById(valueId)
                    .orElseThrow(() -> new RuntimeException("AttributeValue not found"));

            ProductAttribute pa = new ProductAttribute();
            pa.setVariant(variant);
            pa.setAttributeValue(value);

            productAttributeRepository.save(pa);
            values.add(value);
        }

        // Générer le SKU automatiquement
        String sku = generateSku(product.getName(), values);
        variant.setSku(sku);

        // recharger avec les relations
        ProductVariant saved = productVariantRepository.save(variant);

        return productVariantMapper.toDto(saved);
    }

    @Override
    public List<ProductVariantResponseDto> getAllProductVariants() {
        return productVariantRepository.findAll()
                .stream()
                .map(productVariantMapper::toDto)
                .toList();
    }

    @Override
    public ProductVariantResponseDto getById(Long id) {
        ProductVariant variant = productVariantRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product Variant introuvable"));
        return productVariantMapper.toDto(variant);
    }

    @Override
    public List<ProductVariantResponseDto> getByProduct(Long productId) {
        return productVariantRepository.findByProductId(productId)
                .stream()
                .map(productVariantMapper::toDto)
                .toList();
    }

    @Override
    public ProductVariantResponseDto update(Long id, ProductVariantUpdateRequestDto dto) {
        ProductVariant productVariant = productVariantRepository.findById(id)
                .orElseThrow(()-> new RuntimeException("Product variant not found"));

        if(dto.getPrice() != null) {
            productVariant.setPrice(dto.getPrice());
        }
        if(dto.getStock() != null) {
            productVariant.setStock(dto.getStock());
        }

        if(dto.getGender() != null) {
            productVariant.setGender(dto.getGender());
        }
        return productVariantMapper.toDto(productVariantRepository.save(productVariant));
    }

    @Override
    public List<ProductVariantResponseDto> getTop3ByProductCategoryAndGender(Long productCategoryId, Gender gender) {
        return productVariantRepository.findTop3ByProduct_ProductCategory_IdAndGender(productCategoryId, gender)
                .stream()
                .map(productVariantMapper::toDto)
                .toList();
    }

    @Override
    public Page<ProductVariantResponseDto> getVariants(
            Gender gender,
            Long subCategoryId,
            int page,
            int size,
            String sortField,
            String sortDir) {

        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        // Requête paginée côté repository
        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndCategoryAndSubCategory(gender, subCategoryId, pageRequest);

        // On mappe vers DTO pour ne pas exposer l'entité directement
        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByGender(
        Gender gender,
        int page,
        int size,
        String sortField,
        String sortDir) {

            // On détermine la direction du tri
            Sort.Direction direction = Sort.Direction.ASC;
            if ("desc".equalsIgnoreCase(sortDir)) {
                direction = Sort.Direction.DESC;
            }

            // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
            // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
            Sort sort;
            if ("name".equalsIgnoreCase(sortField)) {
                sort = Sort.by(direction, "product.name");
            } else if ("price".equalsIgnoreCase(sortField)) {
                sort = Sort.by(direction, "price");
            } else {
                // Tri par défaut
                sort = Sort.by(direction, "product.name");
            }

            PageRequest pageRequest = PageRequest.of(page, size, sort);

            // Requête paginée côté repository
            Page<ProductVariant> variantsPage = productVariantRepository
                    .findByGender(gender, pageRequest);

            // On mappe vers DTO pour ne pas exposer l'entité directement
            return variantsPage.map(productVariantMapper::toDto);

    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByCategoryGender(Gender gender, Long categoryId, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        // Requête paginée côté repository
        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndCategory(gender, categoryId, pageRequest);

        // On mappe vers DTO pour ne pas exposer l'entité directement
        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByProductCategoryGender(Gender gender, Long productCategoryId, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        // Requête paginée côté repository
        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndProductCategory(gender, productCategoryId, pageRequest);

        // On mappe vers DTO pour ne pas exposer l'entité directement
        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByBrandsAndGender(Gender gender, List<Long> brandIds, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndProduct_Brand_IdIn(gender, brandIds, pageRequest);

        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndCategoryId(Gender gender, Long categoryId, List<Long> brandIds, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndProduct_Category_IdAndProduct_Brand_IdIn(gender, categoryId, brandIds, pageRequest);

        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndSubCategoryId(Gender gender, Long subCategoryId, List<Long> brandIds, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndProduct_SubCategory_IdAndProduct_Brand_IdIn(gender, subCategoryId, brandIds, pageRequest);

        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndProductCategoryId(Gender gender, Long productCategoryId, List<Long> brandIds, int page, int size, String sortField, String sortDir) {
        // On détermine la direction du tri
        Sort.Direction direction = Sort.Direction.ASC;
        if ("desc".equalsIgnoreCase(sortDir)) {
            direction = Sort.Direction.DESC;
        }

        // Si on trie par un champ de ProductVariant, on peut l'utiliser directement
        // Si on trie par un champ du produit (ex: name), on doit utiliser Sort.by("product.name")
        Sort sort;
        if ("name".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "product.name");
        } else if ("price".equalsIgnoreCase(sortField)) {
            sort = Sort.by(direction, "price");
        } else {
            // Tri par défaut
            sort = Sort.by(direction, "product.name");
        }

        PageRequest pageRequest = PageRequest.of(page, size, sort);

        Page<ProductVariant> variantsPage = productVariantRepository
                .findByGenderAndProduct_ProductCategory_IdAndProduct_Brand_IdIn(gender, productCategoryId, brandIds, pageRequest);

        return variantsPage.map(productVariantMapper::toDto);
    }

    @Override
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGender(Gender gender) {
        List<Object[]> results = productVariantRepository.countVariantsByBrandForGender(gender);

        // Transformation en DTO
        return results.stream()
                .map(row -> new BrandVariantCountResponseDto(
                        ((Number) row[0]).longValue(),      // brandId
                        (String) row[1],                     // brandName
                        ((Number) row[2]).longValue()       // variantCount
                ))
                .collect(Collectors.toList());
    }

    @Override
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndCategory(Gender gender, Long categoryId) {
        List<Object[]> results = productVariantRepository.countVariantsByBrandForGenderAndCategory(gender, categoryId);
        return results
                .stream()
                .map(row -> new BrandVariantCountResponseDto(
                        ((Number) row[0]).longValue(),      // brandId
                        (String) row[1],                     // brandName
                        ((Number) row[2]).longValue()       // variantCount
                ))
                .collect(Collectors.toList());
    }

    @Override
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndSubCategory(Gender gender, Long subCategoryId) {
        List<Object[]> results = productVariantRepository.countVariantsByBrandForGenderAndSubCategory(gender, subCategoryId);
        return results
                .stream()
                .map(row -> new BrandVariantCountResponseDto(
                        ((Number) row[0]).longValue(),      // brandId
                        (String) row[1],                     // brandName
                        ((Number) row[2]).longValue()       // variantCount
                ))
                .collect(Collectors.toList());
    }

    @Override
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndProductCategory(Gender gender, Long productCategoryId) {
        List<Object[]> results = productVariantRepository.countVariantsByBrandForGenderAndProductCategory(gender, productCategoryId);
        return results
                .stream()
                .map(row -> new BrandVariantCountResponseDto(
                        ((Number) row[0]).longValue(),      // brandId
                        (String) row[1],                     // brandName
                        ((Number) row[2]).longValue()       // variantCount
                ))
                .collect(Collectors.toList());
    }

    @Override
    public void delete(Long id) {
        ProductVariant productVariant = productVariantRepository.findById(id)
                .orElseThrow(()-> new RuntimeException("Product variant not found"));

        productVariantRepository.delete(productVariant);
    }

    private String generateSku(String productName, List<AttributeValue> values) {
        String productPart = normalize(productName);

        String attributesPart = values.stream()
                .sorted(Comparator.comparing(v -> v.getAttribute().getName()))
                .map(v -> normalize(v.getValue()))
                .collect(Collectors.joining("-"));

        return productPart + "-" + attributesPart;
    }

    private String normalize(String input) {
        return input.toUpperCase()
                .replaceAll("[^A-Z0-9 ]", "");
    }
}
