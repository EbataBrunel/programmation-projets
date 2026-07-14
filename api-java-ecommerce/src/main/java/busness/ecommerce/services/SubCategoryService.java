package busness.ecommerce.services;

import busness.ecommerce.dto.SubCategoryRequestDto;
import busness.ecommerce.dto.SubCategoryResponseDto;
import busness.ecommerce.entity.Category;

import java.util.List;

public interface SubCategoryService {
    // CREATE
    SubCategoryResponseDto createSubCategory(SubCategoryRequestDto dto);

    // READ
    List<SubCategoryResponseDto> getAllSubCategories();

    // GET
    SubCategoryResponseDto getSubCategoryById(Long id);

    // GET
    List<SubCategoryResponseDto> getSubCategoriesByCategory(Long categoryId);

    // UPDATE
    SubCategoryResponseDto updateSubCategory(Long id, SubCategoryRequestDto dto);

    // DELETE
    void deleteSubCategory(Long id);
}
