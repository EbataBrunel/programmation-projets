package eajc.group.apv.mapper;

import eajc.group.apv.dto.NewsRequestDto;
import eajc.group.apv.dto.NewsResponseDto;
import eajc.group.apv.entity.News;
import org.springframework.stereotype.Component;

@Component
public class NewsMapper {

    public News toEntity(NewsRequestDto dto, String filename){

        News news = new News();

        news.setTitle(dto.getTitle().trim());
        news.setContent(dto.getContent().trim());

        news.setPhoto(filename);

        return  news;
    }

    public NewsResponseDto toDto(News news){

        NewsResponseDto dto = new NewsResponseDto();

        dto.setPublicId(news.getPublicId());
        dto.setCreatedAt(news.getCreatedAt());
        dto.setTitle(news.getTitle());
        dto.setContent(news.getContent());
        dto.setPhoto(news.getPhoto());

        return  dto;

    }
}
