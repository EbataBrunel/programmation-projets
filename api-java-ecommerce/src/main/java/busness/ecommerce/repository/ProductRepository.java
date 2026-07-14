package busness.ecommerce.repository;

import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.entity.Product;
import busness.ecommerce.entity.ProductCategory;
import busness.ecommerce.entity.SubCategory;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByProductCategoryId(Long productCategoryId);
}
