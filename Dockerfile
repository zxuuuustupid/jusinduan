FROM ruby:3.2

# 安装 Jekyll
RUN gem install jekyll bundler && \
    gem install jekyll-email-protect && \
    gem install webrick && \
    gem install kramdown-parser-gfm

# 设置工作目录
WORKDIR /srv/jekyll

# 复制项目文件
COPY . .

# 安装依赖
RUN bundle install

# 暴露端口
EXPOSE 4000

# 启动 Jekyll 服务
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--port", "4000"]
