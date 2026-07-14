package busness.ecommerce.services;

import busness.ecommerce.dto.CategoryRequestDto;
import busness.ecommerce.dto.CategoryResponseDto;

import java.util.List;

public interface CategoryService {
    // CREATE
    CategoryResponseDto createCategory(CategoryRequestDto dto);

    // READ
    List<CategoryResponseDto> getAllCategories();

    // GET
    CategoryResponseDto getCategoryById(Long id);

    // UPDATE
    CategoryResponseDto updateCategory(Long id, CategoryRequestDto dto);

    // DELETE
    void deleteCategory(Long id);
}
