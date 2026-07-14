package busness.ecommerce.repository;

import busness.ecommerce.entity.Category;
import busness.ecommerce.entity.SubCategory;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SubCategoryRepository extends JpaRepository<SubCategory, Long> {
    List<SubCategory> findByCategoryId(Long categoryId);
}
