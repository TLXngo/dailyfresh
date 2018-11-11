$(function(){

	var $li = $('.slide_pics li');
	var len = $li.length;
	var $prev = $('.prev');
	var $next = $('.next');
	// 下一个Li的index
	var nowli = 0;
	// 被替换的index
	var preli = 0;

	// 让第一张在最前面
	$li.not(':first').css({
		left:760
	});

	// 循环添加 each
	$li.each(function(index, el) {

		// 元素节点添加
		var $sli = $('<li>');
		if(index==0){
			$sli.addClass('active');
		}

		$sli.appendTo('.points');
	});

	// 点击 切换
	$points = $('.points li');

	$points.click(function(){
		preli = nowli;
		nowli = $(this).index();

		move();

		$(this).addClass('active').siblings().removeClass('active');

	});

	$prev.click(function(){
		preli = nowli;
		nowli --;

		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');

	});

	$next.click(function(){
		preli = nowli;
		nowli ++;
		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');

	});

	$('.slide').mouseenter(function(event) {
		clearInterval(timer);
	});


	$('.slide').mouseleave(function(event) {
		timer = setInterval(auto_play,3000);
	});

	// 自动播放
	timer = setInterval(auto_play,3000);

	function auto_play(){
		preli = nowli;
		nowli ++;
		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');
	}

	function move(){
		if(nowli<0) {
			nowli = len-1;
			preli = 0;

			$li.eq(nowli).css({left:-760});
			$li.eq(preli).animate({left:760}, 300);
			$li.eq(nowli).animate({left:0}, 300);

			return;
		}

		if (nowli>len-1) {
			nowli = 0;
			preli = len-1;
			$li.eq(nowli).css({left:760});
			$li.eq(preli).animate({left:-760}, 300);
			$li.eq(nowli).animate({left:0}, 300);

			return;
		}

		if (nowli>preli) {

			$li.eq(nowli).css({left:760});
			$li.eq(preli).animate({left:-760}, 300);


		}
		else if(nowli<preli){

			$li.eq(nowli).css({left:-760});
			$li.eq(preli).animate({left:760}, 300);

		}

		$li.eq(nowli).animate({left:0}, 300);

	}
});