package eajc.group.apv.services;

import eajc.group.apv.dto.NewsRequestDto;
import eajc.group.apv.dto.NewsResponseDto;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

public interface NewsService {
    // CREATE
    NewsResponseDto createNews(NewsRequestDto dto, MultipartFile photoFile) throws IOException ;

    // READ
    List<NewsResponseDto> getAllNews();

    // GET
    NewsResponseDto getNewsByPublicId(UUID publicId);

    // UPDATE
    public NewsResponseDto updateNews(UUID publicId, NewsRequestDto dto, MultipartFile photoFile) throws IOException ;

    // DELETE
    void deleteNews(UUID publicId);
}
