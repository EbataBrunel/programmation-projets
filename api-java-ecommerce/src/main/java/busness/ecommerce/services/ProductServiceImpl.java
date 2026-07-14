package busness.ecommerce.services;

import busness.ecommerce.dto.ProductRequestDto;
import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.entity.*;
import busness.ecommerce.enums.ProductSource;
import busness.ecommerce.enums.RoleName;
import busness.ecommerce.mapper.ProductMapper;
import busness.ecommerce.mapper.UserMapper;
import busness.ecommerce.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService {

    private final CategoryRepository categoryRepository;
    private final SubCategoryRepository subCategoryRepository;
    private final ProductCategoryRepository productCategoryRepository;
    private  final BrandRepository brandRepository;
    private final ProductMapper productMapper;
    private final ProductRepository productRepository;
    private final UserService userService;

    @Override
    public ProductResponseDto createProduct(ProductRequestDto dto) {
        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));

        SubCategory subCategory = subCategoryRepository.findById(dto.getSubCategoryId())
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));

        ProductCategory productcategory = productCategoryRepository.findById(dto.getProductCategoryId())
                .orElseThrow(() -> new RuntimeException("Product Category not found"));

        Brand brand = brandRepository.findById(dto.getBrandId())
                .orElseThrow(() -> new RuntimeException("Brand not found"));

        User currentUser = userService.getCurrentUser();
        /*
        boolean canSell =
                currentUser.getRoles().stream()
                        .anyMatch(r -> r.getName() == RoleName.ROLE_SELLER
                                || r.getName() == RoleName.ROLE_ADMIN);

        if (!canSell) {
            throw new AccessDeniedException("Vous n'êtes pas autorisé à vendre");
        }
        */
        Product product = productMapper.toEntity(dto, category, subCategory, productcategory, currentUser, brand);

        Product saved = productRepository.save(product);

        return productMapper.toDto(saved);
    }

    @Override
    public List<ProductResponseDto> getAllProducts() {
        return productRepository.findAll()
                .stream()
                .map(productMapper::toDto)
                .toList();
    }

    @Override
    public ProductResponseDto getProductById(Long id) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));
        return productMapper.toDto(product);
    }

    @Override
    public List<ProductResponseDto> getProductByPCategory(Long productCategoryId) {

        return productRepository.findByProductCategoryId(productCategoryId)
                .stream()
                .map(productMapper::toDto)
                .toList();
    }

    @Override
    public ProductResponseDto updateProduct(Long id, ProductRequestDto dto) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));

        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));

        SubCategory subCategory = subCategoryRepository.findById(dto.getSubCategoryId())
                .orElseThrow(() -> new RuntimeException("SubCategory not found"));

        ProductCategory productCategory = productCategoryRepository.findById(dto.getProductCategoryId())
                .orElseThrow(() -> new RuntimeException("Product Category not found"));

        Brand brand = brandRepository.findById(dto.getBrandId())
                .orElseThrow(() -> new RuntimeException("Brand not found"));

        User currentUser = userService.getCurrentUser();
        System.out.println(currentUser.hasRole("ADMIN"));
        /*
        if (product.getSource() == ProductSource.ADMIN &&
                !currentUser.hasRole("ADMIN")) {
            throw new AccessDeniedException("Produit réservé à l'admin");
        }

        if (product.getSource() == ProductSource.SELLER &&
                !product.getOwner().getId().equals(currentUser.getId())) {
            throw new AccessDeniedException("Ce produit ne vous appartient pas");
        }*/

        product.setName(dto.getName());
        product.setDescription(dto.getDescription());
        product.setPrice(dto.getPrice());
        product.setSource(dto.getSource());
        product.setCategory(category);
        product.setSubCategory(subCategory);
        product.setProductCategory(productCategory);
        product.setBrand(brand);

        return productMapper.toDto(productRepository.save(product));
    }

    @Override
    public void deleteProduct(Long id) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));

        productRepository.delete(product);
    }

}
