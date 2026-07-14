package busness.ecommerce.repository;

import busness.ecommerce.entity.ProductAttribute;
import busness.ecommerce.entity.ProductVariant;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductAttributeRepository extends JpaRepository<ProductAttribute, Long> {
    List<ProductAttribute> findByVariant(ProductVariant variant);
}
